from flask import Flask, render_template, request
import sqlite3






conn = sqlite3.connect("cocktails.db")
cocktails = conn.execute(
      "SELECT * FROM cocktails;"
  )
  
for cocktail in cocktails:
  print(cocktail)

