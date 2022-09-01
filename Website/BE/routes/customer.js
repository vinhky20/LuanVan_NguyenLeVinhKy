module.exports = function (app) {
    let customersCtrl = require('../controllers/CustomersController.js');

    // todoList Routes
    app.route('/customers')
        .get(customersCtrl.get)
        .post(customersCtrl.store);

    app.route('/customers/:customerId')
        .get(customersCtrl.detail)
        .put(customersCtrl.update)
        .delete(customersCtrl.delete);
};