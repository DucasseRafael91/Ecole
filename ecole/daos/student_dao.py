# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class StudentDao(Dao[Student]):

    def create(self, student: Student) -> int:
        """Crée en BD l'entité Person puis Student correspondant à student

        :param student: instance de Student à créer
        :return: l'id du Student inséré en BD (0 si échec)
        """
        try:
            with Dao.connection.cursor() as cursor:

                if(student.address):
                    # Création de la Address
                    sql_address = """
                                                           INSERT INTO address (street, city, postal_code)
                                                           VALUES (%s, %s, %s)
                                                           """
                    cursor.execute(sql_address,
                                   (student.address.street, student.address.city, student.address.postal_code))

                    # Récupération de l'id de la Person créée
                    address_id = cursor.lastrowid
                else:
                    address_id = None

                # Création de la Person
                sql_person = """
                    INSERT INTO person (first_name, last_name, age, id_address)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_person, (student.first_name, student.last_name, student.age, address_id))

                # Récupération de l'id de la Person créée
                person_id = cursor.lastrowid
                student.person_id = person_id  # mettre à jour l'objet Student

                # Création du Student lié à cette Person
                sql_student = """
                    INSERT INTO student (id_person)
                    VALUES (%s)
                """
                cursor.execute(sql_student, (person_id,))

                # Récupération de l'id du Student
                student_id = cursor.lastrowid

            # Validation de la transaction
            Dao.connection.commit()
            return student_id

        except Exception as e:
            import traceback
            print("Erreur lors de la création :", type(e).__name__, e)
            traceback.print_exc()
            Dao.connection.rollback()
            return 0

    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        student_nbr: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM student INNER JOIN person ON person.id_person = student.id_person WHERE student_nbr=%s"
            cursor.execute(sql, (student_nbr,))
            record = cursor.fetchone()
        if record is not None:
            student = Student(
                record['first_name'],
                record['last_name'],
                record['age']
            )

            student.student_nbr = record['student_nbr']
        else:
            student = None

        return student

    def read_all(self) -> List[Student]:
        """Renvoie toutes les adresses présentes dans la table 'address'."""
        students: List[Student] = []
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM student"
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            student = Student(record['first_name'],record['last_name'],record['age']
            )
            address.id = record['id_address']
            addresses.append(address)

        return addresses

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Course correspondant à course

        :param address: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    UPDATE student
                    SET id_person=%s
                    WHERE student_nbr=%s
                """
                cursor.execute(sql, (
                    student.students_nb,
                    student.student_nbr
                ))

            Dao.connection.commit()

            # cursor.rowcount : nombre de lignes affectées
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la mise à jour :", e)
            Dao.connection.rollback()
            return False

    def delete(self, id_student: int) -> bool:
        """Supprime en BD l'entité Course correspondant à id_course

        :param id_course: id du cours à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:

                sql = "DELETE FROM student WHERE student_nbr=%s"
                cursor.execute(sql, (id_student,))

            # Validation de la suppression
            Dao.connection.commit()

            # Si aucune ligne supprimée
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la suppression :", e)
            Dao.connection.rollback()
            return False

