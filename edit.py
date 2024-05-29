from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
import sys
import numpy as np
import cv2

def time_to_seconds(time_str):
    # Convert time in format 'hh:mm:ss' to seconds
    parts = time_str.split(':')
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

def draw_triangle(frame, width, height, color):
    # Define the vertices of the triangle
    vertices = np.array([[0, height], [width // 2, 0], [width, height]])
    
    # Create a black background with the same size as the frame
    mask = np.zeros_like(frame)
    
    # Create a filled triangle on the mask
    cv2.fillPoly(mask, [vertices], (255, 255, 255))
    
    # Apply the mask to the color (red in this case)
    masked_color = cv2.bitwise_and(color, mask)
    
    # Apply the inverse mask to the frame
    inverse_mask = cv2.bitwise_not(mask)
    masked_frame = cv2.bitwise_and(frame, inverse_mask)
    
    # Add the masked color and masked frame together
    frame_with_triangle = cv2.add(masked_frame, masked_color)
    
    return frame_with_triangle



def insert_red_triangle(video_clip, start_time, end_time):
    # Calculate dimensions of the red triangle
    triangle_width = video_clip.w // 4
    triangle_height = video_clip.h // 5
    
    # Apply the drawing function to each frame between start and end time
    modified_clip = video_clip.fl(lambda gf, t: draw_triangle(gf(t), triangle_width, triangle_height, (255, 0, 0)) if start_time <= t < end_time else gf(t))
    
    return modified_clip

def insert_white_square(video_clip):
    # Create a white square clip
    square_size = 200
    square = ColorClip(size=(square_size, square_size), color=(255, 255, 255), duration=video_clip.duration)
    
    # Set the position of the square clip
    square = square.set_position(("right", "bottom"))
    
    # Overlap the square clip onto the video clip
    return CompositeVideoClip([video_clip, square])

def main(input_path, start_time, end_time, output_path):
    # Load the input video clip
    video_clip = VideoFileClip(input_path)
    
    # Insert red triangle between start and end time
    video_clip = insert_red_triangle(video_clip, start_time, end_time)
    
    # Insert white square for full duration
    video_clip = insert_white_square(video_clip)
    
    # Write the modified video clip to the output file
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <input_video> <start_time> <end_time> <output_video>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    start_time = time_to_seconds(sys.argv[2])  # Convert start time to seconds
    end_time = time_to_seconds(sys.argv[3])    # Convert end time to seconds
    output_path = sys.argv[4]
    
    main(input_path, start_time, end_time, output_path)
