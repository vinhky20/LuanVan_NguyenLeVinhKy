let express = require('express');
let app = express();
const bodyParser = require('body-parser');
let port = process.env.PORT || 5000;

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

let clinics = require('./routes/clinic')
let customers = require('./routes/customer')
let services = require('./routes/service')
let timeslots = require('./routes/timeslot')
let bookings = require('./routes/booking')
let reviews = require('./routes/review')
let auth = require('./routes/auth')


clinics(app)
customers(app)
services(app)
timeslots(app)
bookings(app)
reviews(app)
auth(app)

app.use(function (req, res) {
    res.status(404).send({ url: req.originalUrl + ' not found' })
})

app.listen(port);

console.log('RESTful API server started on: ' + port);
