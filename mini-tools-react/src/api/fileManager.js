import api from './axios';
import axios from "axios";

export const uploadFile = async (file, folder = "uploads") => {
  // Step 1: Request presigned URL from File Manager
  const res = await api.post("/file-manager/generate-upload-url", {
    file_name: file.name,
    folder,
  });

  const { upload_url, key } = res.data;

  // Step 2: Upload directly to S3
  await axios.put(upload_url, file, {
    headers: {
      'Content-Type': ''  // 👈 override default to match unsigned request
    }
  });

  return { data: { key } }; // match old return format
};

export const getDownloadUrl = (key) => {
  return api.get(`/file-manager/download-url/${encodeURIComponent(key)}`);
};

export const deleteFile = (key) => {
  return api.delete(`/file-manager/delete/${encodeURIComponent(key)}`);
};
