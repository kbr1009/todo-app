from src.domain.exercisetypes.if_exercise_type_repository import IExerciseTypeRepository
from src.domain.exercisetypes.exercise_type import ExerciseType


class ExerciseTypeDomainService:
    def __init__(self, exercise_type_repository: IExerciseTypeRepository):
        self._exercise_type_repository = exercise_type_repository

    def is_duplicated_user_by_exercise_type_name(self, exercise_type: ExerciseType) -> bool:
        """
        指定された種目名が重複しているかどうかをチェックします。
        :param exercise_type: チェックする筋トレ種目オブジェクト
        :return: 種目名が重複していればTrue、そうでなければFalse
        """
        return self._exercise_type_repository.find_by_exercise_type_name(
            exercise_type.exercise_type_name.value) is not None
