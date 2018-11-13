rm exports-db.tar.gz
rm exports-db.tar.gz.enc
tar cvfz exports-db.tar.gz exports-db
openssl enc -aes-256-cbc -in exports-db.tar.gz -out exports-db.tar.gz.enc

