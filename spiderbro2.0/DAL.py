#! /usr/bin/env python
import MySQLdb
import logging as log
import configuration

class DAL:
    def get_db_con(self):
        con = MySQLdb.connect(self.config.host, self.config.user, self.config.pwd, self.config.schema)
        return con

    def __init__(self):
        self.config = configuration.get_args()
        try:
            # test connection, throw error if not valid
            con = self.get_db_con()
            con.close()
            log.debug("Connected to db")
        except:
            log.error("Couldn't connect to db")

