import { useState, useEffect } from "react";
import { analyzeResume } from "./api";
import "./App.css"; // Import styles
import jsPDF from "jspdf";

export default function App() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [score, setScore] = useState("");
  const [strengths, setStrengths] = useState("");
  const [weaknesses, setWeaknesses] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  // ✅ Load saved history from localStorage on page load
  useEffect(() => {
    const savedHistory = JSON.parse(localStorage.getItem("resumeHistory")) || [];
    setHistory(savedHistory);
  }, []);

  const handleAnalyze = async () => {
    setError(null);
    setScore("");
    setStrengths("");
    setWeaknesses("");
    setLoading(true);

    if (!resume) {
      setError("Please upload a resume.");
      setLoading(false);
      return;
    }

    const result = await analyzeResume(resume, jobDesc);
    setLoading(false);

    if (result.error) {
      setError(result.error);
    } else {
      setScore(result.score);
      setStrengths(result.strengths);
      setWeaknesses(result.weaknesses);

      // ✅ Save the result in history
      const newHistory = [
        ...history,
        { score: result.score, strengths: result.strengths, weaknesses: result.weaknesses, timestamp: new Date().toISOString() }
      ];
      setHistory(newHistory);
      localStorage.setItem("resumeHistory", JSON.stringify(newHistory));
    }
  };

  // ✅ Function to Clear History
  const clearHistory = () => {
    localStorage.removeItem("resumeHistory");
    setHistory([]);
  };

  return (
    <div className="container">
      <div className="card">
        <h1>Resume Analyzer</h1>
        <p>Upload your resume and paste a job description to get a match score.</p>

        <label className="file-upload">
          Upload Resume
          <input type="file" accept=".pdf,.docx" onChange={(e) => setResume(e.target.files[0])} />
        </label>

        <textarea
          className="job-desc"
          placeholder="Paste job description here..."
          onChange={(e) => setJobDesc(e.target.value)}
        ></textarea>

        <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {error && <p className="error">⚠️ {error}</p>}

        {score && (
          <div className="result">
            <h2>Score: <span className="score">{score}</span></h2>

            <h3>Strengths:</h3>
            <p>{strengths}</p>

            <h3>Areas for Improvement:</h3>
            <p>{weaknesses}</p>

            <h3>Missing Skills:</h3>
            <p>{missingSkills}</p>

            <h3>Suggested Improvements:</h3>
            <p>{improvements}</p>
            <button className="download-btn" onClick={handleDownloadPDF}>
              Download Report (PDF)
            </button>
          </div>
        )}
      </div>

      {/* ✅ History Section */}
      {history.length > 0 && (
        <div className="history">
          <h3>Past Analyses</h3>
          <button className="clear-btn" onClick={clearHistory}>Clear History</button>
          {history.map((entry, index) => (
            <div key={index} className="history-entry">
              <p><strong>Date:</strong> {new Date(entry.timestamp).toLocaleString()}</p>
              <p><strong>Score:</strong> {entry.score}</p>
              <p><strong>Strengths:</strong> {entry.strengths}</p>
              <p><strong>Weaknesses:</strong> {entry.weaknesses}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
