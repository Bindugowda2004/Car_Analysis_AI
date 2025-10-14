import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Home, RefreshCw } from 'lucide-react';
import axios from 'axios';
import { API } from '@/App';
import { toast } from 'sonner';

const Dashboard = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/analysis/history`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
      toast.error('Failed to load analysis history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div>
      <nav className="dashboard-nav">
        <div className="nav-logo" data-testid="dashboard-logo">Car Analysis AI</div>
        <div className="nav-actions">
          <button
            className="nav-button secondary"
            onClick={() => navigate('/')}
            data-testid="home-btn"
          >
            <Home size={20} />
            Home
          </button>
          <button
            className="nav-button"
            onClick={fetchHistory}
            data-testid="refresh-btn"
          >
            <RefreshCw size={20} />
            Refresh
          </button>
        </div>
      </nav>

      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1 className="dashboard-title" data-testid="dashboard-title">Analysis History</h1>
          <p className="dashboard-subtitle" data-testid="dashboard-subtitle">
            View all your previous image analyses and reports
          </p>
        </div>

        {loading ? (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p className="loading-text">Loading history...</p>
          </div>
        ) : history.length === 0 ? (
          <div className="empty-state" data-testid="empty-state">
            <div className="empty-icon">📊</div>
            <h3 className="empty-title">No Analysis Yet</h3>
            <p className="empty-text">Start by analyzing your first image from the home page</p>
            <button
              className="nav-button"
              style={{ marginTop: '2rem' }}
              onClick={() => navigate('/')}
              data-testid="start-analysis-btn"
            >
              Start Analysis
            </button>
          </div>
        ) : (
          <div className="history-grid">
            {history.map((item) => (
              <div
                key={item.id}
                className="history-card"
                onClick={() => navigate(`/analysis/${item.id}`)}
                data-testid={`history-card-${item.id}`}
              >
                <div className="history-header">
                  <span className="history-type" data-testid="analysis-type">
                    {item.analysis_type === 'white_pixel' ? '🔍 White Pixel' : '🚗 Bonnet'}
                  </span>
                  <span className="history-date" data-testid="analysis-date">
                    {formatDate(item.timestamp)}
                  </span>
                </div>
                <div className="history-content">
                  <h3 data-testid="image-name">{item.image_name}</h3>
                  <p className="history-summary" data-testid="analysis-summary">{item.summary}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;