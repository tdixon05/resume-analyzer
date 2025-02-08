import { useState } from "react";
import { analyzeResume } from "./api";

export default function App() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [score, setScore] = useState("");

  const handleAnalyze = async () => {
    if (!resume) return alert("Please upload a resume.");
    const result = await analyzeResume(resume, jobDesc);
    if (result.error) return alert(result.error);
    setScore(result.score);
  };

  return (
    <div>
      <input type="file" accept=".pdf,.docx" onChange={(e) => setResume(e.target.files[0])} />
      <textarea placeholder="Paste job description" onChange={(e) => setJobDesc(e.target.value)}></textarea>
      <button onClick={handleAnalyze}>Analyze</button>
      <h2>Score: {score}</h2>
    </div>
  );
}
