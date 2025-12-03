#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()

    print(school.get_course_by_id(1))
    print(school.get_course_by_id(3))
    print(school.get_course_by_id(8))
    print(school.get_address_by_id(1))
    print(school.get_address_by_id(2))
    print(school.get_address_by_id(3))

    # school.delete_course_by_id(2)

    # course_updated = school.get_course_by_id(4)
    # course_updated.name = "Mathématiques avancées"
    # school.update_course(course_updated)

    # address_updated = school.get_address_by_id(1)
    # address_updated.city = "Bayonne"
    # school.update_address(address_updated)


if __name__ == '__main__':
    main()
