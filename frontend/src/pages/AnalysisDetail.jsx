import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Image as ImageIcon, AlertCircle, CheckCircle, FileText } from 'lucide-react';
import axios from 'axios';
import { API } from '@/App';
import { toast } from 'sonner';

const AnalysisDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API}/analysis/${id}`);
        setAnalysis(response.data);
      } catch (error) {
        console.error('Error fetching analysis:', error);
        toast.error('Failed to load analysis details');
        navigate('/dashboard');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchAnalysis();
    }
  }, [id, navigate]);

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="loading-spinner" style={{ minHeight: '100vh' }}>
        <div className="spinner"></div>
        <p className="loading-text">Loading analysis...</p>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  return (
    <div>
      <nav className="dashboard-nav">
        <div className="nav-logo" data-testid="detail-logo">Car Analysis AI</div>
        <button
          className="nav-button secondary"
          onClick={() => navigate('/dashboard')}
          data-testid="back-to-dashboard-btn"
        >
          View All Analyses
        </button>
      </nav>

      <div className="detail-container">
        <button className="back-button" onClick={() => navigate(-1)} data-testid="back-btn">
          <ArrowLeft size={20} />
          Back
        </button>

        <div className="detail-card">
          <div className="detail-header">
            <h1 className="detail-title" data-testid="detail-title">
              {analysis.analysis_type === 'white_pixel' ? 'White Pixel Analysis' : 'Car Bonnet Analysis'}
            </h1>
            <div className="detail-meta">
              <div className="meta-item">
                <span className="meta-label">Image Name</span>
                <span className="meta-value" data-testid="detail-image-name">{analysis.image_name}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Analysis Date</span>
                <span className="meta-value" data-testid="detail-date">{formatDate(analysis.timestamp)}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Analysis ID</span>
                <span className="meta-value" data-testid="detail-id">{analysis.id}</span>
              </div>
            </div>
          </div>

          {analysis.analysis_type === 'white_pixel' ? (
            <>
              <div className="detail-section">
                <h2 className="section-title">
                  <span className="section-icon">📊</span>
                  Pixel Analysis
                </h2>
                <div className="info-grid">
                  <div className="info-card">
                    <div className="info-label">White Pixels</div>
                    <div className="info-value" data-testid="white-pixel-count">{analysis.white_pixel_count.toLocaleString()}</div>
                  </div>
                  <div className="info-card">
                    <div className="info-label">Total Pixels</div>
                    <div className="info-value" data-testid="total-pixels">{analysis.total_pixels.toLocaleString()}</div>
                  </div>
                  <div className="info-card">
                    <div className="info-label">Percentage</div>
                    <div className="info-value" data-testid="percentage">{analysis.percentage}%</div>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h2 className="section-title">
                  <span className="section-icon">📝</span>
                  Analysis Result
                </h2>
                <div className="report-text" data-testid="analysis-result">{analysis.analysis_result}</div>
              </div>
            </>
          ) : (
            <>
              <div className="detail-section">
                <h2 className="section-title">
                  <span className="section-icon">🎨</span>
                  Car Information
                </h2>
                <div className="info-grid">
                  <div className="info-card">
                    <div className="info-label">Car Color</div>
                    <div className="info-value" data-testid="car-color">{analysis.car_color}</div>
                  </div>
                  <div className="info-card">
                    <div className="info-label">Condition</div>
                    <div className="info-value" data-testid="condition">{analysis.condition}</div>
                  </div>
                  <div className="info-card">
                    <div className="info-label">Recommendation</div>
                    <div className="info-value" data-testid="wash-repaint">{analysis.wash_or_repaint}</div>
                  </div>
                </div>
              </div>

              {analysis.issues && analysis.issues.length > 0 && (
                <div className="detail-section">
                  <h2 className="section-title">
                    <AlertCircle className="section-icon" />
                    Identified Issues
                  </h2>
                  <ul className="issue-list" data-testid="issues-list">
                    {analysis.issues.map((issue, index) => (
                      <li key={index} className="issue-item" data-testid={`issue-${index}`}>
                        ⚠️ {issue}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {analysis.recommendations && analysis.recommendations.length > 0 && (
                <div className="detail-section">
                  <h2 className="section-title">
                    <CheckCircle className="section-icon" />
                    Recommendations
                  </h2>
                  <ul className="recommendation-list" data-testid="recommendations-list">
                    {analysis.recommendations.map((rec, index) => (
                      <li key={index} className="recommendation-item" data-testid={`recommendation-${index}`}>
                        ✓ {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="detail-section">
                <h2 className="section-title">
                  <FileText className="section-icon" />
                  Detailed Diagnostic Report
                </h2>
                <div className="report-text" data-testid="detailed-report">{analysis.detailed_report}</div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalysisDetail;