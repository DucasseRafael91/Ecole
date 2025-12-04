# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address correspondant à address

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    INSERT INTO address (street, city, postal_code)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (address.street, address.city, address.postal_code))

                # Récupération de l'id généré
                address_id = cursor.lastrowid

            # Validation de l'insertion
            Dao.connection.commit()
            return address_id

        except Exception as e:
            print("Erreur lors de la création :", e)
            Dao.connection.rollback()
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

    def read_all(self) -> List[Address]:
        """Renvoie toutes les adresses présentes dans la table 'address'."""
        addresses: List[Address] = []
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address"
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
            addresses.append(address)

        return addresses

    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité Course correspondant à course

        :param address: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    UPDATE address
                    SET street=%s, city=%s, postal_code=%s
                    WHERE id_address=%s
                """
                cursor.execute(sql, (
                    address.street,
                    address.city,
                    address.postal_code,
                    address.id
                ))

            Dao.connection.commit()

            # cursor.rowcount : nombre de lignes affectées
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la mise à jour :", e)
            Dao.connection.rollback()
            return False

    def delete(self, id_address: int) -> bool:
        """Supprime en BD l'entité Course correspondant à id_course

        :param id_course: id du cours à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:

                sql = "DELETE FROM address WHERE id_address=%s"
                cursor.execute(sql, (id_address,))

            # Validation de la suppression
            Dao.connection.commit()

            # Si aucune ligne supprimée
            return cursor.rowcount > 0

        except Exception as e:
            print("Erreur lors de la suppression :", e)
            Dao.connection.rollback()
            return False

