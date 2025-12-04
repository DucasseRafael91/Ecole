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
        """Crée en BD l'entité Address correspondant à address

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    INSERT INTO teacher (hiring_date, id_person)
                    VALUES (%s, %s)
                """
                cursor.execute(sql, (teacher.hiring_date, teacher.person_id))

                # Récupération de l'id généré
                teacher_id = cursor.lastrowid

            # Validation de l'insertion
            Dao.connection.commit()
            return teacher_id

        except Exception as e:
            print("Erreur lors de la création :", e)
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

