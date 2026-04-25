import pytest
import numpy as np
import torch
import torch.nn as nn
from pathlib import Path

# Mock LSTM model for testing
class LSTMModel(nn.Module):
    def __init__(self, input_size=5, hidden_size=128, num_layers=2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        output = self.fc(last_hidden)
        return self.sigmoid(output)

@pytest.fixture
def lstm_model():
    """Fixture to create LSTM model"""
    model = LSTMModel(input_size=5, hidden_size=128, num_layers=2)
    model.eval()
    return model

@pytest.fixture
def sample_data():
    """Fixture to create sample test data"""
    # Shape: (batch_size, sequence_length, features)
    return torch.randn(10, 30, 5)

class TestLSTMModel:
    
    def test_model_initialization(self, lstm_model):
        """Test model initializes correctly"""
        assert lstm_model is not None
        assert isinstance(lstm_model.lstm, nn.LSTM)
        assert isinstance(lstm_model.fc, nn.Linear)
    
    def test_model_forward_pass(self, lstm_model, sample_data):
        """Test forward pass produces correct output shape"""
        with torch.no_grad():
            output = lstm_model(sample_data)
        
        assert output.shape == (10, 1)
        assert torch.all(output >= 0) and torch.all(output <= 1)
    
    def test_model_output_range(self, lstm_model, sample_data):
        """Test output is in valid probability range [0, 1]"""
        with torch.no_grad():
            output = lstm_model(sample_data)
        
        assert torch.all(output >= 0.0)
        assert torch.all(output <= 1.0)
    
    def test_batch_processing(self, lstm_model):
        """Test model handles different batch sizes"""
        batch_sizes = [1, 8, 16, 32]
        
        for batch_size in batch_sizes:
            data = torch.randn(batch_size, 30, 5)
            with torch.no_grad():
                output = lstm_model(data)
            
            assert output.shape == (batch_size, 1)
    
    def test_sequence_length_flexibility(self, lstm_model):
        """Test model handles different sequence lengths"""
        sequence_lengths = [10, 30, 60, 100]
        batch_size = 8
        
        for seq_len in sequence_lengths:
            data = torch.randn(batch_size, seq_len, 5)
            with torch.no_grad():
                output = lstm_model(data)
            
            assert output.shape == (batch_size, 1)
    
    def test_gradient_flow(self, lstm_model, sample_data):
        """Test gradients flow correctly through model"""
        lstm_model.train()
        optimizer = torch.optim.Adam(lstm_model.parameters())
        loss_fn = nn.BCELoss()
        
        output = lstm_model(sample_data)
        target = torch.randint(0, 2, (10, 1)).float()
        loss = loss_fn(output, target)
        
        loss.backward()
        
        for param in lstm_model.parameters():
            if param.requires_grad:
                assert param.grad is not None
        
        optimizer.step()
    
    def test_model_eval_mode(self, lstm_model):
        """Test model switches to eval mode correctly"""
        lstm_model.train()
        assert lstm_model.training == True
        
        lstm_model.eval()
        assert lstm_model.training == False
    
    def test_input_validation(self, lstm_model):
        """Test model rejects invalid inputs"""
        invalid_data = torch.randn(10, 30, 3)  # Wrong feature size
        
        with pytest.raises((RuntimeError, IndexError)):
            with torch.no_grad():
                lstm_model(invalid_data)
    
    def test_reproducibility(self, sample_data):
        """Test model produces consistent outputs with same seed"""
        torch.manual_seed(42)
        model1 = LSTMModel()
        model1.eval()
        
        torch.manual_seed(42)
        model2 = LSTMModel()
        model2.eval()
        
        with torch.no_grad():
            out1 = model1(sample_data)
            out2 = model2(sample_data)
        
        assert torch.allclose(out1, out2, atol=1e-6)
    
    @pytest.mark.parametrize("hidden_size,num_layers", [(64, 1), (128, 2), (256, 3)])
    def test_model_configurations(self, sample_data, hidden_size, num_layers):
        """Test different model configurations"""
        model = LSTMModel(input_size=5, hidden_size=hidden_size, num_layers=num_layers)
        model.eval()
        
        with torch.no_grad():
            output = model(sample_data)
        
        assert output.shape == (10, 1)
        assert torch.all(output >= 0) and torch.all(output <= 1)

class TestDataProcessing:
    
    def test_feature_normalization(self):
        """Test feature normalization"""
        data = np.array([[100, 50, 30, 10, 5],
                         [200, 75, 60, 20, 10]])
        
        # Normalize to [0, 1]
        normalized = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
        
        assert np.all(normalized >= 0)
        assert np.all(normalized <= 1)
    
    def test_sequence_windowing(self):
        """Test sequence windowing for LSTM"""
        data = np.arange(100).reshape(100, 1)
        window_size = 30
        
        windows = []
        for i in range(len(data) - window_size):
            windows.append(data[i:i+window_size])
        
        assert len(windows) == len(data) - window_size
        assert windows[0].shape == (window_size, 1)

class TestModelPersistence:
    
def test_model_save_load(self, lstm_model, tmp_path):
        """Test model can be saved and loaded"""
        model_path = tmp_path / "test_model.pth"
        
        torch.save(lstm_model.state_dict(), model_path)
        assert model_path.exists()
        
        # Load model
        loaded_model = LSTMModel()
        loaded_model.load_state_dict(torch.load(model_path))
        loaded_model.eval()
        
        # Test loaded model works
        test_data = torch.randn(5, 30, 5)
        with torch.no_grad():
            output = loaded_model(test_data)
        
        assert output.shape == (5, 1)