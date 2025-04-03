import api from './axios';

export const compressRoyaltyReport = (s3Key) => {
  return api.post('/royalty-compressor/compress', {
    s3_key: s3Key,
  });
};
