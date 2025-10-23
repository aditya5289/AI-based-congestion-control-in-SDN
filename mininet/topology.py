# Simple Mininet topology that starts iperf traffic between hosts
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
import time

class SimpleTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')

        self.addLink(h1, s1, bw=10)
        self.addLink(h2, s1, bw=10)
        self.addLink(s1, s2, bw=5)
        self.addLink(h3, s2, bw=10)
        self.addLink(h4, s2, bw=10)

if __name__ == '__main__':
    topo = SimpleTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink, switch=OVSSwitch)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.start()
    h1, h3 = net.get('h1','h3')
    print('Starting iperf server on h3')
    h3.cmd('iperf -s &')
    time.sleep(1)
    print('Starting iperf client on h1 to h3 (10s)')
    print(h1.cmd('iperf -c 10.0.0.3 -t 10 -i 1'))
    CLI(net)
    net.stop()
