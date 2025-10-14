import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Image as ImageIcon, Car } from 'lucide-react';
import axios from 'axios';
import { API } from '@/App';
import { toast } from 'sonner';

const HomePage = () => {
  const navigate = useNavigate();
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [analysisType, setAnalysisType] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleCardClick = (type) => {
    setAnalysisType(type);
    setShowUploadModal(true);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setSelectedFile(file);
      } else {
        toast.error('Please select an image file');
      }
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
    } else {
      toast.error('Please drop an image file');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      toast.error('Please select a file first');
      return;
    }

    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const endpoint = analysisType === 'white-pixel' 
        ? `${API}/analyze/white-pixels` 
        : `${API}/analyze/bonnet`;
      
      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('Analysis completed successfully!');
      setShowUploadModal(false);
      setSelectedFile(null);
      
      // Navigate to the analysis detail page
      navigate(`/analysis/${response.data.id}`);
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const closeModal = () => {
    setShowUploadModal(false);
    setSelectedFile(null);
    setAnalysisType(null);
  };

  return (
    <div className="landing-hero">
      <div className="hero-content">
        <h1 className="hero-title" data-testid="hero-title">Car Analysis AI</h1>
        <p className="hero-subtitle" data-testid="hero-subtitle">
          Advanced AI-powered image analysis for automotive inspection and diagnostics
        </p>

        <div className="analysis-cards">
          <div 
            className="analysis-card" 
            onClick={() => handleCardClick('white-pixel')}
            data-testid="white-pixel-card"
          >
            <span className="card-icon">🔍</span>
            <h2 className="card-title">White Pixel Detection</h2>
            <p className="card-description">
              Upload any image to identify and analyze white pixel concentration for quality assessment
            </p>
          </div>

          <div 
            className="analysis-card" 
            onClick={() => handleCardClick('bonnet')}
            data-testid="bonnet-analysis-card"
          >
            <span className="card-icon">🚗</span>
            <h2 className="card-title">Car Bonnet Analysis</h2>
            <p className="card-description">
              AI-powered analysis of car condition, color identification, and maintenance recommendations
            </p>
          </div>
        </div>

        <button
          className="nav-button secondary"
          style={{ marginTop: '3rem' }}
          onClick={() => navigate('/dashboard')}
          data-testid="view-history-btn"
        >
          View Analysis History
        </button>
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="upload-overlay" onClick={closeModal}>
          <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={closeModal} data-testid="close-modal-btn">
              ×
            </button>
            
            <h2 className="modal-title" data-testid="modal-title">
              {analysisType === 'white-pixel' ? 'White Pixel Detection' : 'Car Bonnet Analysis'}
            </h2>
            <p className="modal-subtitle" data-testid="modal-subtitle">
              {analysisType === 'white-pixel'
                ? 'Upload an image to detect white pixels'
                : 'Upload a car bonnet image for AI analysis'}
            </p>

            <div
              className={`dropzone ${dragOver ? 'drag-over' : ''}`}
              onClick={() => document.getElementById('file-input').click()}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              data-testid="dropzone"
            >
              <div className="dropzone-icon">
                <Upload size={48} />
              </div>
              <p className="dropzone-text">Drag & drop your image here</p>
              <p className="dropzone-subtext">or click to browse</p>
              <input
                id="file-input"
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
                data-testid="file-input"
              />
            </div>

            {selectedFile && (
              <div className="selected-file" data-testid="selected-file">
                <div className="file-info">
                  <span className="file-icon">📁</span>
                  <span className="file-name">{selectedFile.name}</span>
                </div>
                <button
                  className="remove-file"
                  onClick={() => setSelectedFile(null)}
                  data-testid="remove-file-btn"
                >
                  ×
                </button>
              </div>
            )}

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={!selectedFile || isAnalyzing}
              data-testid="analyze-btn"
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze Image'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;