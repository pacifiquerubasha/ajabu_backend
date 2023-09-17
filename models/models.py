from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from lib.database import Base
import uuid
from enum import Enum


class FriendShipStatus(Enum):
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    BLOCKED = 4

class Friend(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    friend_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user = relationship("User", back_populates="friends", foreign_keys=[user_id])
    friend = relationship("User", back_populates="friends", foreign_keys=[friend_id])


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    profile_picture = Column(String, nullable=True)
    is_verified = Column(String, default=False)
    verification_code = Column(String, nullable=True)

    post = relationship("Post", back_populates="user")
    comment = relationship("Comment", back_populates="user")
    friends = relationship("Friend", back_populates="user", foreign_keys=[Friend.user_id])

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    image = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="post")
    comment = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    user = relationship("User", back_populates="comment")
    post = relationship("Post", back_populates="comment")



# class FriendRequest(Base):
#     __tablename__ = 'friend_requests'
#     id = Column(Integer, primary_key=True, index=True)
#     from_user_id = Column(Integer, ForeignKey('users.id'))
#     to_user_id = Column(Integer, ForeignKey('users.id'))
#     status = Column(Integer, default=FriendShipStatus.PENDING)
#     created_at = Column(DateTime, default=func.current_timestamp())
#     updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
   
#     users = relationship("User", back_populates="friend_requests", foreign_keys=[from_user_id])
#     friends = relationship("User", back_populates="friend_requests", foreign_keys=[to_user_id])


# class Group(Base):
#     __tablename__ = 'groups'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(String)
#     image = Column(String)
#     creator_id = Column(Integer, ForeignKey('users.id'))

#     users = relationship("User", back_populates="groups")
#     group_members = relationship("GroupMember", back_populates="groups")
#     group_messages = relationship("GroupMessages", back_populates="groups")
#     group_invitations = relationship("GroupInvitation", back_populates="groups")


# class GroupMember(Base):
#     __tablename__ = 'group_members'
#     id = Column(Integer, primary_key=True, index=True)
#     group_id = Column(Integer, ForeignKey('groups.id'))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     joined_at = Column(DateTime)

#     groups = relationship("Group", back_populates="group_members")
#     users = relationship("User", back_populates="group_members")


# class GroupInvitation(Base):
#     __tablename__ = 'group_invitations'
#     id = Column(Integer, primary_key=True, index=True)
#     group_id = Column(Integer, ForeignKey('groups.id'))
#     from_user_id = Column(Integer, ForeignKey('users.id'))
#     to_user_id = Column(Integer, ForeignKey('users.id'))
#     status = Column(Integer, default=FriendShipStatus.PENDING)
#     created_at = Column(DateTime, default=func.current_timestamp())
#     updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

#     groups = relationship("Group", back_populates="group_invitations")
#     users = relationship("User", back_populates="group_invitations", foreign_keys=[from_user_id])
#     to_users = relationship("User", back_populates="group_invitations", foreign_keys=[to_user_id])



# class GroupMessages(Base):
#     __tablename__ = 'group_messages'
#     id = Column(Integer, primary_key=True, index=True)
#     group_id = Column(Integer, ForeignKey('groups.id'))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     message = Column(String)
#     created_at = Column(DateTime, default=func.current_timestamp())

#     groups = relationship("Group", back_populates="group_messages")
#     users = relationship("User", back_populates="group_messages")