const util = require('util');
const mysql = require('mysql');
const db = require('../db.js');

module.exports = {
    get: (req, res) => {
        let sql = 'SELECT * FROM TIMESLOT'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.status(200).json(response)
        })
    },
    detail: (req, res) => {
        let sql = 'SELECT * FROM TIMESLOT WHERE TIMESLOT_ID = ?'
        db.query(sql, [req.params.timeSlotId], (err, response) => {
            if (err) throw err
            res.status(200).json(response[0])
        })
    },
    update: (req, res) => {
        let data = req.body;
        let TIMESLOT_ID = req.params.timeSlotId;
        let sql = 'UPDATE TIMESLOT SET ? WHERE TIMESLOT_ID = ?'
        db.query(sql, [data, TIMESLOT_ID], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Update success!' })
        })
    },
    store: (req, res) => {
        let data = req.body;
        let sql = 'INSERT INTO TIMESLOT SET ?'
        db.query(sql, [data], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Insert success!' })
        })
    },
    delete: (req, res) => {
        let sql = 'DELETE FROM TIMESLOT WHERE TIMESLOT_ID = ?'
        db.query(sql, [req.params.timeSlotId], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Delete success!' })
        })
    }
}
