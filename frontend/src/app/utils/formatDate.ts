const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('en-GB').replace(/,/, '');
};

export default formatDate;
