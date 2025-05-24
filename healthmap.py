import React, { useState, useEffect } from "react";
import {
  AlertTriangle,
  CheckCircle,
  Clock,
  FileText,
  ArrowRight,
  Map,
  BarChart2,
} from "lucide-react";

// API Configuration
const API_BASE_URL = "https://healthmap-m780.onrender.com/api";

const HealthMapAnalyzer = () => {
  const [file, setFile] = useState(null);
  const [mapUrl, setMapUrl] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [serviceStatus, setServiceStatus] = useState("checking");
  const [activeTab, setActiveTab] = useState("map");

  useEffect(() => {
    checkServiceHealth();
    // Simulate progress for demo
    if (loading) {
      const interval = setInterval(() => {
        setUploadProgress((prev) => (prev >= 100 ? 0 : prev + 10));
      }, 500);
      return () => clearInterval(interval);
    }
  }, [loading]);

  const checkServiceHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      setServiceStatus(data.status === "healthy" ? "ready" : "error");
    } catch (err) {
      console.error("Health check error:", err);
      setServiceStatus("error");
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) {
      setError("Please select a file");
      return;
    }
    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please select a CSV file");
      return;
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError("File size must be less than 10MB");
      return;
    }
    setFile(selectedFile);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || serviceStatus !== "ready") return;

    setLoading(true);
    setError(null);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/generate-map`, {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to process file");
      }
      
      const data = await response.json();
      
      if (data.success) {
        // Set the complete URL for the map
        const fullMapUrl = `https://healthmap-m780.onrender.com${data.map_url}`;
        setMapUrl(fullMapUrl);
        console.log("Generated Map URL:", fullMapUrl);
        
        // For demo purposes, we'll create mock analysis results
        // In a real implementation, you'd get this from the API
        setAnalysisResults({
          metrics: [
            { name: "Health Score", value: 85 },
            { name: "Risk Level", value: 25 },
            { name: "Coverage", value: 92 },
          ],
          findings: [
            "Population health metrics show positive trends",
            "Healthcare access has improved by 15%",
            "Preventive care adoption increased",
          ],
          recommendations: [
            "Focus on expanding rural healthcare access",
            "Implement targeted health education programs",
            "Enhance preventive care services",
          ],
        });
      } else {
        throw new Error("Failed to generate map");
      }
    } catch (err) {
      console.error("Submit error:", err);
      setError(err.message || "An error occurred while processing your request");
    } finally {
      setLoading(false);
    }
  };

  const StatusBadge = () => (
    <div
      className={`px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2 ${
        serviceStatus === "ready"
          ? "bg-green-100 text-green-800"
          : serviceStatus === "checking"
          ? "bg-yellow-100 text-yellow-800"
          : "bg-red-100 text-red-800"
      }`}
    >
      {serviceStatus === "ready" ? (
        <>
          <CheckCircle size={16} /> Service Ready
        </>
      ) : serviceStatus === "checking" ? (
        <>
          <Clock size={16} /> Checking Status...
        </>
      ) : (
        <>
          <AlertTriangle size={16} /> Service Unavailable
        </>
      )}
    </div>
  );

  const MetricsCard = ({ metric }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex flex-col gap-2">
        <h3 className="text-sm font-medium text-gray-500">{metric.name}</h3>
        <div className="flex items-end gap-2">
          <span className="text-3xl font-bold">{metric.value}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full"
            style={{ width: `${metric.value}%` }}
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="bg-white/80 backdrop-blur rounded-xl shadow-xl">
          <div className="border-b border-gray-100 p-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-blue-400">
                  Health Map Analyzer
                </h1>
                <p className="text-gray-500 mt-2">
                  Upload your health data to generate insights
                </p>
              </div>
              <StatusBadge />
            </div>
          </div>

          <div className="p-6">
            <form onSubmit={handleSubmit} className="max-w-xl mx-auto">
              <div className="mb-6">
                <div className="rounded-xl border-2 border-dashed border-gray-200 p-8 text-center hover:border-blue-400 transition-colors duration-200">
                  <div className="mx-auto w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4">
                    <FileText className="h-8 w-8 text-blue-500" />
                  </div>
                  <label className="cursor-pointer">
                    <span className="text-sm text-gray-600">
                      Drag and drop your CSV file here, or{" "}
                      <span className="text-blue-500 hover:text-blue-600 font-medium">
                        browse
                      </span>
                    </span>
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileChange}
                      className="hidden"
                      disabled={loading}
                    />
                  </label>
                  <p className="text-xs text-gray-400 mt-2">
                    Maximum file size: 10MB
                  </p>
                </div>
                {file && (
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg flex items-center gap-3">
                    <FileText className="h-5 w-5 text-blue-500" />
                    <span className="text-sm text-blue-700 font-medium">
                      {file.name}
                    </span>
                  </div>
                )}
              </div>

              {error && (
                <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                  <AlertTriangle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading || !file || serviceStatus !== "ready"}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-lg text-white font-medium transition-all duration-200 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Clock className="animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    Generate Analysis
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              {loading && (
                <div className="mt-4">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="text-sm text-gray-500 mt-2 text-center">
                    {uploadProgress}% Complete
                  </p>
                </div>
              )}
            </form>

            {(mapUrl || analysisResults) && (
              <div className="mt-8">
                <div className="border-b border-gray-200 mb-6">
                  <div className="flex gap-6">
                    <button
                      onClick={() => setActiveTab("map")}
                      className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors ${
                        activeTab === "map"
                          ? "border-blue-500 text-blue-600"
                          : "border-transparent text-gray-500 hover:text-gray-700"
                      }`}
                    >
                      <Map className="w-4 h-4" />
                      Health Map
                    </button>
                    <button
                      onClick={() => setActiveTab("analysis")}
                      className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors ${
                        activeTab === "analysis"
                          ? "border-blue-500 text-blue-600"
                          : "border-transparent text-gray-500 hover:text-gray-700"
                      }`}
                    >
                      <BarChart2 className="w-4 h-4" />
                      Analysis
                    </button>
                  </div>
                </div>

                {activeTab === "map" && mapUrl && (
                  <div className="rounded-xl overflow-hidden shadow-lg">
                    <iframe
                      src={mapUrl}
                      title="Generated Health Map"
                      className="w-full h-96 border-0"
                    />
                  </div>
                )}

                {activeTab === "analysis" && analysisResults && (
                  <div className="space-y-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {analysisResults.metrics.map((metric, index) => (
                        <MetricsCard key={index} metric={metric} />
                      ))}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="bg-white rounded-lg shadow-md p-6">
                        <h3 className="text-lg font-semibold mb-4">
                          Key Findings
                        </h3>
                        <ul className="space-y-4">
                          {analysisResults.findings.map((finding, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                                <span className="text-blue-600 text-sm font-medium">
                                  {index + 1}
                                </span>
                              </div>
                              <span className="text-gray-600">{finding}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-white rounded-lg shadow-md p-6">
                        <h3 className="text-lg font-semibold mb-4">
                          Recommendations
                        </h3>
                        <ul className="space-y-4">
                          {analysisResults.recommendations.map((rec, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                                <span className="text-green-600 text-sm font-medium">
                                  {index + 1}
                                </span>
                              </div>
                              <span className="text-gray-600">{rec}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthMapAnalyzer;


