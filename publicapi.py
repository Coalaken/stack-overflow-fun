import graphene

from apps.stackoverflow.schema import Query as StackQuery
from apps.stackoverflow.schema import Mutation as StackMutation
from apps.users.schema import Query as UsersQuery
from apps.users.schema import Mutation as UsersMutation


class Query(StackQuery,
            UsersQuery,
            graphene):
    pass


class Mutation(StackMutation,
               UsersMutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)