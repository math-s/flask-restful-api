#!/bin/bash
echo -e '\033[33;1m Starting test...  \033[m'
echo 
echo 

echo -e '\033[32;1m[GET] http://127.0.0.1:5000/did_number \033[m'
curl -i http://127.0.0.1:5000/did_number

echo -e '\033[32;1m[GET] http://127.0.0.1:5000/did_number_detail/1\033[m'
curl -i http://127.0.0.1:5000/did_number_detail/1

echo -e '\033[32;1m[GET] http://127.0.0.1:5000/did_number_detail/1000 \033[m'
curl -i http://127.0.0.1:5000/did_number_detail/1000 


echo -e '\033[33;1mLogin required, database updating \033[m'
echo 
echo

echo -e '\033[32;1m[POST] http://127.0.0.1:5000/login \033[m'
curl -d '{"email":"email2@email.com","password":"123"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/login

echo -e '\033[32;1m[POST] http://127.0.0.1:5000/add_number \033[m'
curl -d '{
  "currency": "U$",
  "monthyPrice": 0.01,
  "setupPrice": 5.3,
  "value": "+00 00 000000000"
}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/add_number

echo -e '\033[32;1m[PUT] http://127.0.0.1:5000/update_number \033[m'
curl -d '{
  "id":7
  "currency": "U$",
  "monthyPrice": 0.09,
  "setupPrice": 5.3,
  "value": "+11 11 111111111"
}' -H 'Content-Type: application/json' -X PUT http://127.0.0.1:5000/update_number/

echo -e '\033[32;1m[GET] http://127.0.0.1:5000/did_number \033[m'
curl -i http://127.0.0.1:5000/did_number

echo -e '\033[32;1m[DELETE] http://127.0.0.1:5000/delete_number/7 \033[m'
curl -X DELETE  http://127.0.0.1:5000/delete_number/7

echo -e '\033[32;1m[GET] http://127.0.0.1:5000/did_number \033[m'
curl -i http://127.0.0.1:5000/did_number


