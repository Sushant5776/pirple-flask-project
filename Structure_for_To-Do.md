# Structure for To-Do

## Path Hierarchy

### Level 1

1. ToDo - Directory

### Level 2

#### Inside ToDo Directory

1. static - Directory
2. templates - Directory
3. todo.db
4. app.py
5. schema.py
6. model.py

### Level 3

#### Inside static Directory

1. css - Directory

#### Inside templates Directory

1. structure.html
2. index.html
3. termsOfUse.html
4. privacy.html
5. about.html
6. signup.html
7. login.html
8. dashboard.html
9. createList.html
10. list.html

## Requirements of Database

### Level 1

1. main.db - Database
2. todo.db - Database

### Level 2

#### Inside main.db

1. users - Table

#### Inside todo.db

1. listname - Table

### Level 3

#### Inside users Table in main.db

1. id - INTEGER PRIMARY KEY AUTO INCREMENT
2. username - VARCHAR(max_length=60, UNIQUE)
3. password - VARCHAR(max_length=100)
4. registration_date - concerned data and time

#### Inside listname Table in todo.db

1. id - Integer, PRIMARY KEY, AUTO INCREMENT
2. list_item - VARCHAR(max_length=100)
3. done - BOOLEAN

























