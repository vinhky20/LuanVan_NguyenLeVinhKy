const util = require('util')
const mysql = require('mysql')
const db = require('../db.js')

module.exports = {
    get: (req, res) => {
        let sql = 'SELECT * FROM CUSTOMER'
        db.query(sql, (err, response) => {
            if (err) throw err
            res.status(200).json(response)
        })
    },
    detail: (req, res) => {
        let sql = 'SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = ?'
        db.query(sql, [req.params.customerId], (err, response) => {
            if (err) throw err
            res.status(200).json(response[0])
        })
    },
    update: (req, res) => {
        let data = req.body;
        let CUSTOMER_ID = req.params.customerId;
        let sql = 'UPDATE CUSTOMER SET ? WHERE CUSTOMER_ID = ?'
        db.query(sql, [data, CUSTOMER_ID], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Update success!' })
        })
    },
    store: (req, res) => {
        let data = req.body;
        let sql = 'INSERT INTO CUSTOMER SET ?'
        db.query(sql, [data], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Insert success!' })
        })
    },
    delete: (req, res) => {
        let sql = 'DELETE FROM CUSTOMER WHERE CUSTOMER_ID = ?'
        db.query(sql, [req.params.customerId], (err, response) => {
            if (err) throw err
            res.status(200).json({ message: 'Delete success!' })
        })
    }
}
