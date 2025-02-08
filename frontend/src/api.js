export const analyzeResume = async (file, jobDesc) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_desc", jobDesc);
  
    try {
      const res = await fetch(process.env.REACT_APP_BACKEND_URL + "/analyze", {
        method: "POST",
        body: formData,
      });
  
      if (!res.ok) throw new Error("Failed to analyze resume.");
      
      return await res.json();
    } catch (error) {
      console.error("Error:", error);
      return { error: "Analysis failed. Try again later." };
    }
  };
  