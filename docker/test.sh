#!/bin/bash

pytest -v -s test/test_crud_menu.py 
pytest -v -s test/test_crud_submenu.py 
pytest -v -s test/test_crud_dish.py 
pytest -v -s test/test_count.py 