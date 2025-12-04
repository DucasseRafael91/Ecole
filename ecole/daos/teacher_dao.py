# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherDao(Dao[Teacher]):

    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Person puis Student correspondant à student

        :param student: instance de Student à créer
        :return: l'id du Student inséré en BD (0 si échec)
        """
        try:
            with Dao.connection.cursor() as cursor:

                # 1️⃣ Création de la Person
                sql_person = """
                    INSERT INTO person (first_name, last_name, age)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_person, (teacher.first_name, teacher.last_name, teacher.age))

                # Récupération de l'id de la Person créée
                person_id = cursor.lastrowid
                teacher.person_id = person_id  # mettre à jour l'objet Student

                # 2️⃣ Création du Student lié à cette Person
                sql_student = """
                    INSERT INTO teacher (hiring_date,id_person)
                    VALUES (%s, %s)
                """
                cursor.execute(sql_student, (teacher.hiring_date, person_id))

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

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM teacher INNER JOIN person ON person.id_person = teacher.id_person WHERE id_teacher=%s"
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(
                record['first_name'],
                record['last_name'],
                record['age'],
                record['hiring_date']
            )

            teacher.id = record['id_teacher']
        else:
            teacher = None

        return teacher

    def update(self, teacher: Teacher) -> bool:
        """
        Met à jour en BD l'entité Teacher correspondant à teacher.

        :param teacher: enseignant déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    UPDATE teacher
                    SET hiring_date = %s,
                        id_person = %s
                    WHERE id_teacher = %s
                """
                cursor.execute(sql, (
                    teacher.hiring_date,
                    teacher.person_id,
                    teacher.id
                ))

                rows = cursor.rowcount

            Dao.connection.commit()
            return rows > 0

        except Exception as e:
            print("Erreur lors de la mise à jour :", e)
            Dao.connection.rollback()
            return False

    def delete(self, id_teacher: int) -> bool:
        """Supprime en BD l'entité Course correspondant à id_course

        :param id_course: id du cours à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:

                sql = "DELETE FROM teacher WHERE id_teacher=%s"
                cursor.execute(sql, (id_teacher,))

            # Validation de la suppression
            Dao.connection.commit()

            # Si aucune ligne supprimée
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la suppression :", e)
            Dao.connection.rollback()
            return False

