from graphene import (
    Int,
    ObjectType,
    Field,
    String,
    List, 
    Schema,
    Mutation,
)
from graphene_django import DjangoObjectType

from .models import Question, QuestionImage, Answer, AnswerImage
from apps.users.models import User


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer


class QuestionImageType(DjangoObjectType):
    class Meta:
        model = QuestionImage


class AnswerImageType(DjangoObjectType):
    class Meta:
        model = AnswerImage


class Query(ObjectType):
    questoin = Field(QuestionType, id=Int())
    all_questions = List(QuestionType)
    question_images = List(QuestionImageType, id=Int())
    questoin_image = Field(QuestionImageType, id=Int())
    answer = Field(AnswerType, id=Int())
    all_answers = List(AnswerType)
    question_answers = List(AnswerType, id=Int())
    answer_images = List(AnswerImageType, id=Int())
    answer_image = Field(AnswerImageType, id=Int())
    
    def resolve_all_questions(self, info):
        return Question.objects.all()
    
    def resolve_question(sel, info, id):
        # get or None
        return Question.objects.get(id=id)

    def resolve_all_answers(self, info):
        return Answer.objects.all()
    
    def resolve_answer(self, info, id):
        # get or None
        return Answer.objects.get(id=id)
    
    def resolve_question_answers(self, info, id):
        return Answer.objects.filter(question__id=id)

    def resolve_question_images(self, info, id):
        return Question.objects.filter(questoin__id=id)
    
    def resolve_questoin_image(self, info, id):
        return QuestionImage.objects.get(id=id)
    
    def resolve_answer_images(self, info, id):
        return AnswerImage.objects.filter(answer__id=id)
    
    def resolve_answer_image(self, info, id):
        return AnswerImage.objects.get(id=id)


class AddQuestion(Mutation):
    question = Field(QuestionType)
    
    class Arguments:
        user = Int()
        title = String()
        question = String()
    
    def mutate(self, info, user, title, question):
        user = User.objects.get(id=user)
        question = Question(user=user, title=title,question=question)
        question.save()
        return AddQuestion(question=question)


class UpdateQuestoin(Mutation):
    questoin = Field(QuestionType)
    
    class Arguments:
        id = Int()
        title = String()
        question = String()
    
    def mutate(self, info, id, title):
        questoin = Question.objects.get(id=id)
        questoin.title = title
        questoin.question = questoin
        questoin.save()
        return UpdateQuestoin(questoin=questoin)


class AddAnswer(Mutation):
    answer = Field(AnswerType)
    
    class Arguments:
        user = Int()
        question = Int()
        answer = String()

    def mutate(self, info, user, question, answer):
        user = User.objects.get(id=user)
        question = Question.objects.get(id=question)
        answer = Answer(user=user, question=question, answer=answer)
        answer.save()
        return AddAnswer(answer=answer)


class UpdateAnswer(Mutation):
    answer = Field(AnswerType)

    class Arguments:
        id = Int()
        answer = String()

    def mutate(self, info, id, answer):
        answer = Answer.objects.get(id=id)
        answer.answer = answer
        answer.save()
        return UpdateAnswer(answer=answer)


class AddQuestionImage(Mutation):
    image = Field(QuestionImageType)
    
    class Arguments:
        question = Int()
        url = String()
    
    def mutate(self, info, question, url):
        question = Question.objects.get(id=question)
        image = QuestionImage(question=question, url=url)
        image.save()
        return AddQuestionImage(image=image)


class AddAnswerImage(Mutation):
    image = Field(AnswerImageType)
    
    class Arguments:
        answer = Int()
        url = String()
    
    def mutate(self, info, answer, url):
        answer = Answer.objects.get(id=answer)
        image = AnswerImage(answer=answer, url=url)
        image.save()
        return AddAnswerImage(image=image)


class Mutation(ObjectType):
    add_question = AddQuestion.Field()
    update_question = UpdateQuestoin.Field()
    add_question_image = AddQuestionImage.Field()
    add_answer = AddAnswer.Field()
    update_answer = UpdateAnswer.Field()
    add_answer_image = AddQuestionImage.Field()


schema = Schema(query=Query, mutation=Mutation)
