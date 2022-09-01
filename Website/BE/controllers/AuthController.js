const util = require('util')
const mysql = require('mysql')
const db = require('../db.js')

module.exports = {
    clinicLogin: (req, res) => {
        let username = req.body.CLINIC_URN;
        let password = req.body.CLINIC_PWD;
        let sql = 'SELECT * FROM CLINIC WHERE CLINIC_URN = ? AND CLINIC_PWD = ?';
        if (username && password) {
            db.query(sql, [username, password], function (error, results, fields) {
                if (error) throw error;
                if (results.length > 0) {
                    res.status(200).json(results[0])
                } else {
                    res.send('Incorrect Username and/or Password!');
                }
                res.end();
            });
        } else {
            res.send('Please enter Username and Password!');
            res.end();
        }


        // let sql = 'SELECT * FROM CLINIC'
        // db.query(sql, (err, response) => {
        //     if (err) throw err
        //     res.status(200).json(response)
        // })
    },
    customerLogin: (req, res) => {
        let username = req.body.CUSTOMER_URN;
        let password = req.body.CUSTOMER_PWD;
        let sql = 'SELECT * FROM CUSTOMER WHERE CUSTOMER_URN = ? AND CUSTOMER_PWD = ?';
        if (username && password) {
            db.query(sql, [username, password], function (error, results, fields) {
                if (error) throw error;
                if (results.length > 0) {
                    res.status(200).json(results[0])
                } else {
                    res.send('Incorrect Username and/or Password!');
                }
                res.end();
            });
        } else {
            res.send('Please enter Username and Password!');
            res.end();
        }

    }
}