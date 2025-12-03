# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param adress: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address=%s"
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address

    def update(self, course: Address) -> bool:
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

