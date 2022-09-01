module.exports = function (app) {
    let reviewsCtrl = require('../controllers/ReviewsController.js');

    // todoList Routes
    app.route('/reviews')
        .get(reviewsCtrl.get)
        .post(reviewsCtrl.store);

    app.route('/reviews/:reviewClinic&:reviewCustomer')
        .put(reviewsCtrl.update)
        .delete(reviewsCtrl.delete);
};