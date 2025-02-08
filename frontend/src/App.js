import { useState } from "react";
import { analyzeResume } from "./api";
import "./App.css"; // Import styles

export default function App() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [score, setScore] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setError(null);
    setScore("");
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
    }
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

        {error && <p className="error">{error}</p>}

        {score && (
          <div className="result">
            <h2>Score: <span className="score">{score}</span></h2>
          </div>
        )}
      </div>
    </div>
  );
}
