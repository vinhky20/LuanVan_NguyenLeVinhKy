const util = require('util')
const mysql = require('mysql')
const db = require('../db.js')

module.exports = {
    get: (req, res) => {
        let sql = 'SELECT * FROM CLINIC'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.status(200).json(response)
        })
    },
    detail: (req, res) => {
        let sql = 'SELECT * FROM CLINIC WHERE CLINIC_ID = ?'
        db.query(sql, [req.params.clinicId], (err, response) => {
            if (err) throw err
            res.status(200).json(response[0])
        })
    },
    update: (req, res) => {
        let data = req.body;
        let CLINIC_ID = req.params.clinicId;
        let sql = 'UPDATE CLINIC SET ? WHERE CLINIC_ID = ?'
        db.query(sql, [data, CLINIC_ID], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Update success!' })
        })
    },
    store: (req, res) => {
        let data = req.body;
        let sql = 'INSERT INTO CLINIC SET ?'
        db.query(sql, [data], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Insert success!' })
        })
    },
    delete: (req, res) => {
        let sql = 'DELETE FROM CLINIC WHERE CLINIC_ID = ?'
        db.query(sql, [req.params.clinicId], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Delete success!' })
        })
    }
}
