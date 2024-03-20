from src.application.exercisetypes.commands.create_new_exercise_request import CreateNewExerciseTypeRequest
from src.application.exercisetypes.commands.if_create_new_exercise_type_command import ICreateNewExerciseCommand
from src.domain.exercisetypes.exercise_type import ExerciseType
from src.domain.exercisetypes.exercise_type_domain_service import ExerciseTypeDomainService
from src.domain.exercisetypes.exercise_type_value_objects import ExerciseTypeName, CategoryTag
from src.domain.exercisetypes.if_exercise_type_repository import IExerciseTypeRepository
from src.domain.shard.domain_exception import DomainException


class CreateNewExerciseTypeCommand(ICreateNewExerciseCommand):
    def __init__(self, repository: IExerciseTypeRepository):
        self._repository = repository

    def execute(self, request: CreateNewExerciseTypeRequest) -> None:

        # タグをドメインオブジェクトに変換しリスト化する
        category_tags: list[CategoryTag] = [CategoryTag(i) for i in request.category_tags]

        # ドメインオブジェクトの組み立て
        new_exercise_type = ExerciseType.create_new_exercise_type(
            exercise_type_name=ExerciseTypeName(request.exercise_type_name),
            category_tags=category_tags,
            user_id=request.user_id)

        # ドメインサービスによる所在チェック
        domain_service: ExerciseTypeDomainService = ExerciseTypeDomainService(self._repository)
        if domain_service.is_duplicated_user_by_exercise_type_name(new_exercise_type):
            raise DomainException(f"'{request.exercise_type_name}' は既に登録されているようです。")

        # データ永続のセーブ
        self._repository.save(new_exercise_type)
