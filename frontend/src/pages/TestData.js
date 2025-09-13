export const mockApplications = [
  {
    id: 1,
    company_name: "Google",
    position: "Frontend Developer",
    applied_date: "2025-08-01",
    interview_one: "2025-08-05",
    interview_two: "2025-08-12",
    offer_date: "2025-08-20",
    status: "offer",
    resume_url: "https://example.com/resume-google.pdf",
    resume_file: "GoogleResume.pdf",
  },
  {
    id: 2,
    company_name: "Meta",
    position: "Product Designer",
    applied_date: "2025-07-20",
    interview_one: "2025-07-28",
    interview_two: null,
    offer_date: null,
    status: "interview",
    resume_url: "https://example.com/resume-meta.pdf",
    resume_file: "MetaResume.pdf",
  },
  {
    id: 3,
    company_name: "OpenAI",
    position: "Research Engineer",
    applied_date: "2025-09-01",
    interview_one: null,
    interview_two: null,
    offer_date: null,
    status: "applied",
    resume_url: null,
    resume_file: "Resume.pdf",
  },
];

export const mockResume = {
  title: "Default Resume",
  created_at: "2025-06-15",
  file_url: "https://example.com/default-resume.pdf",
};
