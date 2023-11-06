import graphene
from graphene_django import DjangoObjectType

from apps.users.schema import Query as UserQuery
from apps.users.schema import Mutation as UserMutation
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)
    all_users = graphene.List(UserType)
    
    def resolve_user(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
    
    def resolve_all_users(self, info):
        return User.objects.all()


class AddUser(graphene.Mutation):
    user = graphene.Field(UserType)
    
    class Arguments:
        email = graphene.String()
        password = graphene.String()
    
    def mutate(self, info, email, password=None):
        user = User(email=email)
        if password:
            user.set_password(password)
        user.save()
        return AddUser(user=user)


class UpdateUser(graphene.ObjectType):
    user = graphene.Field(UserType)
    
    class Arguments:
        id = graphene.ID()
        email = graphene.String()
        password = graphene.String()
        
    def mutate(self, info, id, email=None, password=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return None
        if email:
            user.email = email
            
        if password:
            user.password = password
        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    user = graphene.Field(UserType)
    
    class Arguments:
        id = graphene.ID()
        
    def mutate(self, info, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return None
        user.delete()
        return DeleteUser(user=user)
            

class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)