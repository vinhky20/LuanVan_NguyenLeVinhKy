module.exports = function (app) {
    let servicesCtrl = require('../controllers/ServicesController.js');

    // todoList Routes
    app.route('/services')
        .get(servicesCtrl.get)
        .post(servicesCtrl.store);

    app.route('/services/:serviceId')
        .get(servicesCtrl.detail)
        .put(servicesCtrl.update)
        .delete(servicesCtrl.delete);
};