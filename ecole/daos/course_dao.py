# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Address correspondant à address

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    INSERT INTO course (name, start_date, end_date, id_teacher)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (course.name,course.start_date,course.end_date,course.teacher))

                # Récupération de l'id généré
                course_id = cursor.lastrowid

            # Validation de l'insertion
            Dao.connection.commit()
            return course_id
        except Exception as e:
            print("Erreur lors de la création :", e)
            Dao.connection.rollback()
            return 0

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
        else:
            course = None

        return course

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    UPDATE course
                    SET name=%s, start_date=%s, end_date=%s
                    WHERE id_course=%s
                """
                cursor.execute(sql, (
                    course.name,
                    course.start_date,
                    course.end_date,
                    course.id
                ))

            Dao.connection.commit()

            # cursor.rowcount : nombre de lignes affectées
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la mise à jour :", e)
            Dao.connection.rollback()
            return False

    def delete(self, id_course: int) -> bool:
        """Supprime en BD l'entité Course correspondant à id_course

        :param id_course: id du cours à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:

                sql_delete_takes = "DELETE FROM takes WHERE id_course=%s"
                cursor.execute(sql_delete_takes, (id_course,))

                sql = "DELETE FROM course WHERE id_course=%s"
                cursor.execute(sql, (id_course,))

            # Validation de la suppression
            Dao.connection.commit()

            # Si aucune ligne supprimée
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la suppression :", e)
            Dao.connection.rollback()
            return False

