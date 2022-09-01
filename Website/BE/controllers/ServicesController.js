const util = require('util')
const mysql = require('mysql')
const db = require('../db.js')

module.exports = {
    get: (req, res) => {
        let sql = 'SELECT * FROM SERVICE'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.status(200).json(response)
        })
    },
    detail: (req, res) => {
        let sql = 'SELECT * FROM SERVICE WHERE SERVICE_ID = ?'
        db.query(sql, [req.params.serviceId], (err, response) => {
            if (err) throw err
            res.status(200).json(response[0])
        })
    },
    update: (req, res) => {
        let data = req.body;
        let SERVICE_ID = req.params.serviceId;
        let sql = 'UPDATE SERVICE SET ? WHERE SERVICE_ID = ?'
        db.query(sql, [data, SERVICE_ID], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Update success!' })
        })
    },
    store: (req, res) => {
        let data = req.body;
        let sql = 'INSERT INTO SERVICE SET ?'
        db.query(sql, [data], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Insert success!' })
        })
    },
    delete: (req, res) => {
        let sql = 'DELETE FROM SERVICE WHERE SERVICE_ID = ?'
        db.query(sql, [req.params.serviceId], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Delete success!' })
        })
    }
}
