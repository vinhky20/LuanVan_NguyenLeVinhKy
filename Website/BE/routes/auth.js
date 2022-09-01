module.exports = function (app) {
    let authCtrl = require('../controllers/AuthController.js');

    // todoList Routes
    app.route('/login/clinic')
        .post(authCtrl.clinicLogin);

    app.route('/login/customer')
        .post(authCtrl.customerLogin);
};