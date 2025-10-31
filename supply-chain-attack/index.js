module.exports = {
  formatBookingDate: (date) => new Date(date).toISOString(),
  calculateNights: (checkIn, checkOut) => Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24)),
  validateRoomType: (type) => ['standard', 'deluxe', 'suite'].includes(type)
};
