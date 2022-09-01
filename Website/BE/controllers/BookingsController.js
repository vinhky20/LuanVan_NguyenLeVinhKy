const util = require('util')
const mysql = require('mysql')
const db = require('../db.js')

module.exports = {
    get: (req, res) => {
        let sql = 'SELECT * FROM BOOKING'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.status(200).json(response)
        })
    },
    detail: (req, res) => {
        let sql = 'SELECT * FROM BOOKING WHERE BOOKING_ID = ?'
        db.query(sql, [req.params.bookingId], (err, response) => {
            if (err) throw err
            res.status(200).json(response[0])
        })
    },
    update: (req, res) => {
        let data = req.body;
        let BOOKING_ID = req.params.bookingId;
        let sql = 'UPDATE BOOKING SET ? WHERE BOOKING_ID = ?'
        db.query(sql, [data, BOOKING_ID], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Update success!' })
        })
    },
    store: (req, res) => {
        let data = req.body;
        let sql = 'INSERT INTO BOOKING SET ?'
        db.query(sql, [data], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Insert success!' })
        })
    },
    delete: (req, res) => {
        let sql = 'DELETE FROM BOOKING WHERE BOOKING_ID = ?'
        db.query(sql, [req.params.bookingId], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Delete success!' })
        })
    }
}
