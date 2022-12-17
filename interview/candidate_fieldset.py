#因为在admin中有大量的fieldsets，所以专门放在新的脚本里

# 当页面的东西太多时，就可以用fieldsets来进行分组，同时也可以一行显示多个字段，只需要将放一行的字段变成元组就好。
fieldsets = (
    (None, {
        'fields': (("username", "city", "phone",), ("email", "apply_position"), ("born_address", "gender",
                                                                                 "candidate_remark"),
                   ("bachelor_school", "master_school", "doctor_school"),
                   ("major", "degree", "test_score_of_general_ability", "paper_score"),),
    }),
    ('第一轮面试记录', {
        'fields': (("first_score", "first_learning_ability", "first_professional_competency"),
                   ("first_advantage", "first_disadvantage", "first_result"),
                   ("first_recommend_position", "first_interviewer_user", "first_remark"),
                   ),
    }),
    ('第二轮面试记录', {
        'fields': (("second_score", "second_learning_ability", "second_professional_competency"),
                   ("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"),
                   ("second_advantage", "second_disadvantage", "second_result"),
                   ("second_recommend_position", "second_interviewer_user", "second_remark"),
                   ),
    }),
    ('第三轮面试记录', {
        'fields': (
            ("hr_score", "hr_responsibility", "hr_communication_ability"), ("hr_logic_ability", "hr_potential",
                                                                            "hr_stability"),
            ("hr_advantage", "hr_disadvantage", "hr_result"),
            ("hr_interviewer_user", "hr_remark", "creator", "last_editor"),)
    }),
)
# 新需求，要求一面面试官只能填写一面反馈，二面面试官只能填写二面反馈，
default_list_first = ((None, {
    'fields': (("username", "city", "phone",), ("email", "apply_position"), ("born_address", "gender",
                                                                             "candidate_remark"),
               ("bachelor_school", "master_school", "doctor_school"),
               ("major", "degree", "test_score_of_general_ability", "paper_score"),),
}),
                      ('第一轮面试记录', {
                          'fields': (("first_score", "first_learning_ability", "first_professional_competency"),
                                     ("first_advantage", "first_disadvantage", "first_result"),
                                     ("first_recommend_position", "first_interviewer_user", "first_remark"),
                                     ),
                      }),
                      )
default_list_second = ((None, {
    'fields': (("username", "city", "phone",), ("email", "apply_position"), ("born_address", "gender",
                                                                             "candidate_remark"),
               ("bachelor_school", "master_school", "doctor_school"),
               ("major", "degree", "test_score_of_general_ability", "paper_score"),),
}),
                       ('第一轮面试记录', {
                           'fields': (("first_score", "first_learning_ability", "first_professional_competency"),
                                      ("first_advantage", "first_disadvantage", "first_result"),
                                      ("first_recommend_position", "first_interviewer_user", "first_remark"),
                                      ),
                       }),
                       ('第二轮面试记录', {
                           'fields': (
                               ("second_score", "second_learning_ability", "second_professional_competency"),
                               ("second_pursue_of_excellence", "second_communication_ability",
                                "second_pressure_score"),
                               ("second_advantage", "second_disadvantage", "second_result"),
                               ("second_recommend_position", "second_interviewer_user", "second_remark"),
                           ),
                       }),

                       )


