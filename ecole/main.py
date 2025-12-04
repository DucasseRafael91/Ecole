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

    # address = Address("10 rue de la Paix", "Paris", 75002)
    # School.create_address(address)

    print(school.get_course_by_id(1))
    print(school.get_course_by_id(3))
    print(school.get_course_by_id(8))
    print(school.get_address_by_id(1))
    print(school.get_address_by_id(2))
    print(school.get_address_by_id(3))
    print(school.get_student_by_id(1))
    print(school.get_student_by_id(2))
    print(school.get_student_by_id(3))
    print(school.get_teacher_by_id(1))
    print(school.get_teacher_by_id(2))
    print(school.get_teacher_by_id(3))


    # school.delete_course_by_id(2)
    # school.delete_address_by_id(4)
    # school.delete_student_by_id(4)

    # course_updated = school.get_course_by_id(4)
    # course_updated.name = "Mathématiques avancées"
    # school.update_course(course_updated)

    # address_updated = school.get_address_by_id(1)
    # address_updated.city = "Bayonne"
    # school.update_address(address_updated)

    # student_updated = school.get_student_by_id(5)
    # student_updated.students_nb = 8
    # school.update_student(student_updated)

    # teacher_updated = school.get_teacher_by_id(6)
    # teacher_updated.person_id = 9
    # school.update_teacher(teacher_updated)


if __name__ == '__main__':
    main()
