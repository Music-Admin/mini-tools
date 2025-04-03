import api from './axios';

export const createSession = (data = {}) => {
  return api.post('/session-manager/create-session', data);
};

export const trackUsage = (sessionId, usageData) => {
  return api.post(`/session-manager/track-usage/${encodeURIComponent(sessionId)}`, usageData);
};

export const getSessionData = (sessionId) => {
  return api.get(`/session-manager/session-data/${encodeURIComponent(sessionId)}`);
};
