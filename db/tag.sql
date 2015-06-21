CREATE TABLE tag
    (
        id INTEGER NOT NULL,
        nom VARCHAR NOT NULL,
        value VARCHAR NOT NULL,
        ecriture_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(ecriture_id) REFERENCES ecriture (id)
    );
