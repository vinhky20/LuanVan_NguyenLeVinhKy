module.exports = function (app) {
    let timeSlotsCtrl = require('../controllers/TimeSlotsController.js');

    // todoList Routes
    app.route('/timeSlots')
        .get(timeSlotsCtrl.get)
        .post(timeSlotsCtrl.store);

    app.route('/timeSlots/:timeSlotId')
        .get(timeSlotsCtrl.detail)
        .put(timeSlotsCtrl.update)
        .delete(timeSlotsCtrl.delete);
};