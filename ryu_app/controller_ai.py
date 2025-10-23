# Simple Ryu app that polls switch stats and calls ML model via REST
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, set_ev_cls
from ryu.lib.packet import packet, ethernet, ipv4, tcp
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub
import requests, json, time

PREDICT_URL = 'http://127.0.0.1:5000/predict'  # backend predict endpoint

class SimpleAIController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleAIController, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        dp = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.logger.info('Register datapath: %s', dp.id)
            self.datapaths[dp.id] = dp
        elif ev.state == DEAD_DISPATCHER:
            if dp.id in self.datapaths:
                del self.datapaths[dp.id]

    def _monitor(self):
        while True:
            for dp_id, dp in list(self.datapaths.items()):
                try:
                    # For demonstration we'll craft synthetic features
                    link_util = 50  # TODO: collect real stats via OFPMP_PORT_STATS
                    queue_len = 20
                    bw_usage = 45
                    features = [link_util, queue_len, bw_usage]
                    resp = requests.post(PREDICT_URL, json={'features': features}, timeout=2)
                    if resp.ok:
                        pred = resp.json().get('prediction')
                        self.logger.info('DP %s prediction=%s', dp_id, pred)
                        if pred == 1:
                            # Example action: install a dummy drop rule or reroute; here we log
                            self.logger.info('Congestion predicted on datapath %s - take action', dp_id)
                    else:
                        self.logger.error('Predict failed: %s', resp.text)
                except Exception as e:
                    self.logger.error('Monitor error: %s', e)
            time.sleep(5)
