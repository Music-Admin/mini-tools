export const countTodayCompressions = (usageLogs) => {
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD

  return usageLogs.filter((log) => {
    if (log.action !== "compress") return false;
    const timestamp = new Date(log.timestamp * 1000).toISOString().slice(0, 10);
    return timestamp === today;
  }).length;
};