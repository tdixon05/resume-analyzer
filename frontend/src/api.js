export const analyzeResume = async (file, jobDesc) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_desc", jobDesc);

  try {
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/analyze`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to analyze resume.");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    return { error: error.message };
  }
};
