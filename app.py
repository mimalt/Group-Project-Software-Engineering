from crypt import methods
from flask import Flask,request, jsonify
import datetime
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from flask_bcrypt import Bcrypt

import src.functions.connection as connection

api = Flask(__name__)
bcrypt = Bcrypt(api)
conn = connection.connect()

import src.functions.test as setupTest
import src.functions.userInfo as userInfo
import src.functions.groupinfo as groupInfo
import src.functions.authorization as auth
import src.entities.pairMeeting as pair
import src.entities.pairings as pairing
from src.entities.Encoder import CustomJSONEncoder
import src.entities.Timeline as timeline
import src.functions.siteFeedback as feedback
import src.entities.developmentGoals as development

import src.entities.interactions as interactions

api.json_encoder=CustomJSONEncoder

api.config["JWT_SECRET_KEY"] = "6ffpCk8fMVddUM6kd9YFwcdD29xup7Ld"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
jwt = JWTManager(api)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity

conn = connection.connect()

# Test Api calls
@api.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@api.route("/api/test")
def test():
    return setupTest.getTestData(conn)

@api.route("/api/test/auth")
@jwt_required()
def testAuth():
    return setupTest.getTestAuthData(current_user)


# Users Api calls
@api.route("/api/profile")
@jwt_required()
def profile():
    return userInfo.testInfo()

##Login Process
## CITE
## Lifted largely from here https://dev.to/nagatodev/how-to-add-login-authentication-to-a-flask-and-react-application-23i7
##

@api.after_request
def refresh(response):
    return auth.refresh_expiring_jwts(response)

# User calls
@api.route('/token',methods=["POST"])
def create_token():
    return auth.login(request)
    
@api.route("/logout",methods=["POST"])
def logout():
    return auth.logout()

@api.route("/api/user/<userID>",methods=["GET"])
@jwt_required()
def user(userID):
    #TODO verify that user ID is an INT
    return userInfo.getUserInfo(int(userID),int(current_user))

@api.route("/api/profile/<userID>",methods=["GET"])
@jwt_required()
def userProfile(userID):
    #TODO verify that user ID is an INT
    return userInfo.getPartUserInfo(int(userID),int(current_user))

@api.route("/api/user/",methods=["POST"])
def newUser():
    return userInfo.newUser(request)

@api.route("/api/user/<userID>",methods=["PUT"])
@jwt_required()
def changeUser(userID):
    #TODO verify that user ID is an INT
    return userInfo.updateUser(request,int(userID),int(current_user))

# @api.route("/api/mentors/feedback",methods=["POST"])
# @jwt_required()
# def addFeedback():
#     #TODO verify that user ID is an INT
#     return userInfo.addFeedback(request,int(current_user))

@api.route("/api/mentors/<menteeID>/request",methods=["PUT"])
@jwt_required()
def acceptRelationship(menteeID):
    #TODO verify that user ID is an INT
    return userInfo.acceptRelationship(request,menteeID,int(current_user))


@api.route("/api/user/search",methods=["POST"]) #post bc get does not alow a body in react
@jwt_required()
def searchUser():
    return userInfo.searchUsers(request,int(current_user))

## The pair meeting Api calls

@api.route("/api/meeting/<meetingID>",methods=["GET"])
@jwt_required()
def getMeetingInfo(meetingID):
    return pair.meetingInfo(conn, meetingID,int(current_user))

@api.route("/api/user/<userID>/meetings")
@jwt_required()
def getAllMeetings(userID):
    return pair.allMeetings(conn, userID)

@api.route("/api/meeting", methods=["POST"])
@jwt_required()
def createNewMeeting():
    return pair.createMeeting(conn, request,int(current_user))

@api.route("/api/meeting/<meetingID>/attendence", methods=["PUT"])
@jwt_required()
def updateUserAttendance(meetingID):
    return pair.updateAttendance(conn, request, meetingID, int(current_user))

@api.route("/api/meeting/<meetingID>/feedback", methods=["POST"])
@jwt_required()
def addMeetingFeedback(meetingID):
    return pair.addFeedback(conn, request, meetingID)

## The group meeting Api calls

@api.route("/api/group",methods=["POST"]) 
@jwt_required()
def newGroup():
    return groupInfo.newGroup(request,int(current_user))

@api.route("/api/group/<groupID>",methods=["GET"])
@jwt_required()
def getGroupID(groupID):
    return groupInfo.getGroupID(request,groupID,int(current_user))

@api.route("/api/group/code/<code>",methods=["GET"])
@jwt_required()
def getGroupCode(code):
    return groupInfo.getGroupCode(request,code,int(current_user))

@api.route("/api/group/<meetingID>/attendance",methods=["POST"])
@jwt_required()
def joinGroup(meetingID):
    return groupInfo.joinMeeting(request,meetingID,int(current_user))

@api.route("/api/group/needed")
@jwt_required()
def getNeeded():
    return groupInfo.getNeeded()
#Interactions part

# @api.route("/api/interactions/<userID>",methods=["GET"])
# @jwt_required()
# def getTimeline(userID):
#     return timeline.getTimeline(request,userID,int(current_user))


# @api.route("/api/interactions",methods=["POST"])
# @jwt_required()
# def addTimeline():
#     return timeline.addMessage(request,int(current_user))

# Site feedback

@api.route("/api/feedback",methods=["POST"])
def addSiteFeedback():
    return feedback.add_feedback(request)

@api.route("/api/feedback",methods=["GET"])
def getSiteFeedback():
    return feedback.get_feedback(request)


    
## Mentor mentee pairings Api calls 

@api.route("/api/mentors/<pairID>/request",methods=["PUT"])
@jwt_required()
def respondToMentorRequest(pairID):
    return pairing.respondMentorRequest(conn, request, pairID, int(current_user))

@api.route("/api/mentors/recommended",methods=["GET"])
@jwt_required()
def findRecommendedMentors():
    return pairing.recommendedMentors(conn, int(current_user))

@api.route("/api/mentors/<userID>/request",methods=["POST"])
@jwt_required()
def requestMentor(userID):
    return pairing.requestMentor(conn, userID, int(current_user))

# I did not notice that there was a feedback fucntion already but this one can also update the feedback
@api.route("/api/mentors/feedback",methods=["POST"])
@jwt_required()
def addMentorFeedback():
    return pairing.addMentorFeedBack(conn, request, int(current_user))



# lets figure this out
@api.route("/api/user/<userID>/goals",methods=["GET"])
@jwt_required()
def getDevelopmentGoals(userID):
    return development.getGoal(conn, userID)

@api.route("/api/user/<userID>/goals/<goalID>",methods=["PUT"])
@jwt_required()
def updateDevelopmentGoal(goalID):
    return development.updateGoal(conn, request, goalID)

@api.route("/api/user/<userID>/subgoals/<subgoalID>",methods=["PUT"])
@jwt_required()
def updateSubGoal(userID,subgoalID):
    return development.updateSubGoal(conn, request, subgoalID)

@api.route("/api/user/<userID>/goals", methods=["POST"])
@jwt_required()
def createGoal(userID):
    return development.createGoal(conn, request, userID)

@api.route("/api/user/<userID>/goals/<goalID>/subgoal",methods=["POST"])
@jwt_required()
def createSubGoal(userID,goalID):
    return development.createSubGoal(conn, request, goalID)

@api.route("/api/user/<userID>/goals/<goalID>",methods=["DEL"])
@jwt_required()
def deleteGoal(goalID):
    return development.deleteGoal(conn, goalID)

@api.route("/api/user/<userID>/subgoals/<subgoalID>",methods=["DEL"])
@jwt_required()
def deleteSubGoal(subgoalID):
    return development.deleteSubGoal(conn, subgoalID)
# Interactions api calls

@api.route("/api/interactions/<otherUser>",methods=["GET"])
@jwt_required()
def getAllInteractions(otherUser):
    return interactions.allInteractions(conn,otherUser, int(current_user))

@api.route("/api/interactions",methods=["POST"])
@jwt_required()
def sendMessage():
    return interactions.sendMessage(conn, request, int(current_user))
