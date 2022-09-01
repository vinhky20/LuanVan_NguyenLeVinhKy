module.exports = function (app) {
    let bookingsCtrl = require('../controllers/BookingsController.js');

    // todoList Routes
    app.route('/bookings')
        .get(bookingsCtrl.get)
        .post(bookingsCtrl.store);

    app.route('/bookings/:bookingId')
        .get(bookingsCtrl.detail)
        .put(bookingsCtrl.update)
        .delete(bookingsCtrl.delete);
};